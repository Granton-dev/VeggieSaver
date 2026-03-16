import json
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.http import JsonResponse
from .models import Vegetable, WasteLog, GardenTip, ScanResult
from .forms import RegisterForm, VegetableForm, WasteLogForm
from .utils import analyze_vegetable_photo, get_smart_tips


# ── AUTH ─────────────────────────────────────────────────────────────────────

def about_veggieguard(request):
    return render(request, 'garden/about_veggieguard.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'garden/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        login(request, user)
        messages.success(request, f'Welcome to VeggieGuard, {user.first_name or user.username}!')
        return redirect('dashboard')
    return render(request, 'garden/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('about_veggieguard')


# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    vegetables = Vegetable.objects.filter(user=request.user)
    recent_scans = ScanResult.objects.filter(user=request.user)[:6]
    recent_waste = WasteLog.objects.filter(user=request.user)[:5]
    total_waste = WasteLog.objects.filter(
        user=request.user
    ).aggregate(Sum('quantity_wasted'))['quantity_wasted__sum'] or 0

    alerts = ScanResult.objects.filter(
        user=request.user,
        freshness_status__in=['caution', 'spoiling', 'spoiled']
    ).order_by('-scanned_at')[:5]

    health_counts = {
        s: vegetables.filter(health_status=s).count()
        for s in ['excellent', 'good', 'fair', 'poor']
    }

    total_scans = ScanResult.objects.filter(user=request.user).count()
    avg_freshness = ScanResult.objects.filter(
        user=request.user
    ).aggregate(Avg('freshness_score'))['freshness_score__avg'] or 0

    context = {
        'vegetables': vegetables,
        'recent_scans': recent_scans,
        'recent_waste': recent_waste,
        'total_waste': total_waste,
        'health_counts': health_counts,
        'veg_count': vegetables.count(),
        'alerts': alerts,
        'total_scans': total_scans,
        'avg_freshness': round(avg_freshness),
    }
    return render(request, 'garden/dashboard.html', context)


# ── SCAN ──────────────────────────────────────────────────────────────────────

@login_required
def scan_vegetable(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        scan = ScanResult(user=request.user, photo=photo)
        scan.save()
        try:
            result = analyze_vegetable_photo(scan.photo.path)
            scan.identified_vegetable = result.get('identified_vegetable', 'Unknown')
            scan.confidence_score = float(result.get('confidence_score', 0))
            scan.freshness_status = result.get('freshness_status', 'unknown')
            scan.freshness_score = int(result.get('freshness_score', 0))
            scan.condition = result.get('condition', 'unknown')
            scan.days_remaining = result.get('days_remaining')
            scan.full_analysis = result.get('full_analysis', '')
            scan.recommendations = result.get('recommendations', '')
            scan.meal_suggestions = result.get('meal_suggestions', '')
            scan.storage_tips = result.get('storage_tips', '')
            scan.raw_ai_response = result
            scan.save()
            return redirect('scan_result', pk=scan.pk)
        except Exception as e:
            scan.delete()
            messages.error(request, f'Analysis failed: {str(e)}. Please try again.')
            return redirect('scan_vegetable')

    recent_scans = ScanResult.objects.filter(user=request.user)[:4]
    return render(request, 'garden/scan.html', {'recent_scans': recent_scans})


@login_required
def scan_result(request, pk):
    scan = get_object_or_404(ScanResult, pk=pk, user=request.user)
    raw = scan.raw_ai_response or {}
    context = {
        'scan': scan,
        'warning_signs': raw.get('warning_signs', []),
        'nutritional_impact': raw.get('nutritional_impact', ''),
        'household_tip': raw.get('household_tip', ''),
    }
    return render(request, 'garden/scan_result.html', context)


@login_required
def scan_history(request):
    scans = ScanResult.objects.filter(user=request.user)
    freshness_filter = request.GET.get('freshness', '')
    if freshness_filter:
        scans = scans.filter(freshness_status=freshness_filter)
    context = {
        'scans': scans,
        'freshness_filter': freshness_filter,
        'freshness_choices': ScanResult.FRESHNESS_CHOICES,
    }
    return render(request, 'garden/scan_history.html', context)


# ── VEGETABLES ────────────────────────────────────────────────────────────────

@login_required
def add_vegetable(request):
    form = VegetableForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        veg = form.save(commit=False)
        veg.user = request.user
        veg.save()
        if not veg.photo:
            catalogue_img = request.POST.get('catalogue_img', '')
            if catalogue_img:
                relative_path = catalogue_img.replace('/media/', '')
                veg.photo = relative_path
                veg.save()

        if veg.photo:
            try:
                result = analyze_vegetable_photo(veg.photo.path)
                veg.ai_analysis = result.get('full_analysis', '')
                veg.health_status = _freshness_to_health(
                    result.get('freshness_status', 'good')
                )
                veg.save()
                ScanResult.objects.create(
                    user=request.user,
                    vegetable=veg,
                    photo=veg.photo,
                    identified_vegetable=result.get('identified_vegetable', veg.name),
                    confidence_score=float(result.get('confidence_score', 0)),
                    freshness_status=result.get('freshness_status', 'fresh'),
                    freshness_score=int(result.get('freshness_score', 100)),
                    condition=result.get('condition', 'healthy'),
                    days_remaining=result.get('days_remaining'),
                    full_analysis=result.get('full_analysis', ''),
                    recommendations=result.get('recommendations', ''),
                    meal_suggestions=result.get('meal_suggestions', ''),
                    storage_tips=result.get('storage_tips', ''),
                    raw_ai_response=result,
                )
                messages.success(request, f'{veg.name} added with AI analysis!')
            except Exception as e:
                messages.warning(request, f'Vegetable added but analysis failed: {e}')
        else:
            messages.success(request, f'{veg.name} added to your garden!')
        return redirect('dashboard')
    return render(request, 'garden/add_vegetable.html', {'form': form})


@login_required
def vegetable_detail(request, pk):
    veg = get_object_or_404(Vegetable, pk=pk, user=request.user)
    if request.method == 'POST' and 'reanalyze' in request.POST:
        if not veg.photo:
            catalogue_img = request.POST.get('catalogue_img', '')
            if catalogue_img:
                relative_path = catalogue_img.replace('/media/', '')
                veg.photo = relative_path
                veg.save()

        if veg.photo:
            try:
                result = analyze_vegetable_photo(veg.photo.path)
                veg.ai_analysis = result.get('full_analysis', '')
                veg.health_status = _freshness_to_health(
                    result.get('freshness_status', 'good')
                )
                veg.save()
                messages.success(request, 'AI analysis updated!')
            except Exception as e:
                messages.error(request, f'Analysis failed: {e}')
        return redirect('vegetable_detail', pk=pk)
    scans = ScanResult.objects.filter(vegetable=veg).order_by('-scanned_at')[:5]
    return render(request, 'garden/vegetable_detail.html', {'veg': veg, 'scans': scans})


# ── WASTE ─────────────────────────────────────────────────────────────────────

@login_required
def waste_log(request):
    form = WasteLogForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()
        messages.success(request, 'Waste logged.')
        return redirect('waste_log')
    logs = WasteLog.objects.filter(user=request.user)
    return render(request, 'garden/waste_log.html', {'form': form, 'logs': logs})


# ── ANALYTICS ─────────────────────────────────────────────────────────────────

@login_required
def analytics(request):
    thirty_days_ago = date.today() - timedelta(days=30)

    waste_by_reason = (
        WasteLog.objects.filter(user=request.user, date__gte=thirty_days_ago)
        .values('reason')
        .annotate(total=Sum('quantity_wasted'))
        .order_by('-total')
    )

    waste_over_time = []
    for i in range(13, -1, -1):
        day = date.today() - timedelta(days=i)
        total = WasteLog.objects.filter(
            user=request.user, date=day
        ).aggregate(Sum('quantity_wasted'))['quantity_wasted__sum'] or 0
        waste_over_time.append({'date': str(day), 'total': total})

    vegetables = Vegetable.objects.filter(user=request.user)
    health_data = [
        {'status': s, 'count': vegetables.filter(health_status=s).count()}
        for s in ['excellent', 'good', 'fair', 'poor']
    ]

    scan_freshness = (
        ScanResult.objects.filter(user=request.user)
        .values('freshness_status')
        .annotate(count=Count('id'))
    )

    freshness_trend = []
    for i in range(13, -1, -1):
        day = date.today() - timedelta(days=i)
        avg = ScanResult.objects.filter(
            user=request.user,
            scanned_at__date=day
        ).aggregate(Avg('freshness_score'))['freshness_score__avg'] or None
        freshness_trend.append({'date': str(day), 'avg': round(avg) if avg else None})

    context = {
        'waste_by_reason_json': json.dumps(list(waste_by_reason)),
        'waste_over_time_json': json.dumps(waste_over_time),
        'health_data_json': json.dumps(health_data),
        'scan_freshness_json': json.dumps(list(scan_freshness)),
        'freshness_trend_json': json.dumps(freshness_trend),
        'total_vegetables': vegetables.count(),
        'total_waste_30d': sum(w['total'] for w in waste_by_reason),
        'total_scans': ScanResult.objects.filter(user=request.user).count(),
    }
    return render(request, 'garden/analytics.html', context)


# ── MONITOR ───────────────────────────────────────────────────────────────────

@login_required
def monitor(request):
    vegetables = Vegetable.objects.filter(user=request.user)
    poor_health = vegetables.filter(health_status__in=['fair', 'poor'])
    recent_scans = ScanResult.objects.filter(user=request.user)[:12]
    alerts = ScanResult.objects.filter(
        user=request.user,
        freshness_status__in=['caution', 'spoiling', 'spoiled']
    ).order_by('-scanned_at')[:10]
    context = {
        'vegetables': vegetables,
        'poor_health': poor_health,
        'recent_scans': recent_scans,
        'alerts': alerts,
    }
    return render(request, 'garden/monitor.html', context)


# ── AJAX ──────────────────────────────────────────────────────────────────────

@login_required
def get_tips_ajax(request):
    veg_names = list(
        Vegetable.objects.filter(user=request.user).values_list('name', flat=True)
    )
    try:
        tips = get_smart_tips(veg_names, request.user)
        return JsonResponse({'success': True, 'tips': tips})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _freshness_to_health(freshness_status):
    mapping = {
        'fresh': 'excellent',
        'good': 'good',
        'caution': 'fair',
        'spoiling': 'poor',
        'spoiled': 'poor',
    }
    return mapping.get(freshness_status, 'good')
