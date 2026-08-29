from django.shortcuts import render, redirect
from django.views import View
from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse
import requests

# Create your views here.


class Home(View):
    def get(self, request, *args, **kwargs):
        context_var = self.context()
        return render(request, "home.html", context_var)

    def context(self):

        context_var = {"data": None}
        return context_var


def meta_auth(request):
    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "response_type": "code",
        "scope": "ads_read,ads_management",
    }
    print(params["client_id"], ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(params["redirect_uri"], ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    meta_url = "https://www.facebook.com/v24.0/dialog/oauth?" + urlencode(params)

    return redirect(meta_url)


def meta_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse(
            {"error": "Missing authorization code"},
            status=400,
        )

    token_url = "https://graph.facebook.com/v24.0/oauth/access_token"

    params = {
        "client_id": settings.META_APP_ID,
        "client_secret": settings.META_APP_SECRET,
        "redirect_uri": settings.META_REDIRECT_URI,
        "code": code,
    }

    response = requests.get(
        token_url,
        params=params,
        timeout=10,
    )

    data = response.json()

    if response.status_code != 200:
        return JsonResponse(
            {
                "error": "Failed to get Meta access token",
                "details": data,
            },
            status=400,
        )

    access_token = data["access_token"]

    return JsonResponse(
        {
            "success": True,
            "access_token": access_token,
        }
    )


class Add_campaign(View):
    def get(self, request, *args, **kwargs):
        context_var = self.context()
        return render(request, "add_campaign.html", context_var)

    def context(self):
        url = "https://graph.facebook.com/v26.0/act_4755523421433857/campaigns"

        params = {
            "access_token": settings.USER_ACCESS_TOKEN,
            "fields": "id,name,status,objective,buying_type,created_time",
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        campaign_datas = response.json()

        context_var = {"campaign_datas": campaign_datas}

        return context_var

    def post(self, request, *args, **kwargs):

        # Get Meta access token from session
        access_token = settings.USER_ACCESS_TOKEN

        if not access_token:
            return render(
                request,
                "add_campaign.html",
                {"error": "Meta access token not found."},
            )

        buying_type = request.POST.get("buying_type")
        name = request.POST.get("name")
        objective = request.POST.get("objective")
        special_ad_category = request.POST.get("special_ad_categories")
        status = request.POST.get("status")

        budget_sharing = request.POST.get("is_adset_budget_sharing_enabled") == "true"

        # Meta API payload
        data = {
            "access_token": access_token,
            "buying_type": buying_type,
            "name": name,
            "objective": objective,
            "special_ad_categories": [special_ad_category],
            "status": status,
            "is_adset_budget_sharing_enabled": budget_sharing,
        }

        print("Sending to Meta:")
        print(data)

        # Meta Campaign API
        url = "https://graph.facebook.com/v26.0/act_4755523421433857/campaigns"

        try:
            response = requests.post(
                url,
                data=data,
                timeout=30,
            )

            response_data = response.json()

            print("Meta Response:")
            print(response_data)

            if response.ok:
                return render(
                    request,
                    "add_campaign.html",
                    {
                        "success": "Campaign created successfully.",
                        "meta_response": response_data,
                    },
                )

            return render(
                request,
                "add_campaign.html",
                {
                    "error": response_data,
                },
            )

        except requests.RequestException as e:
            return render(
                request,
                "add_campaign.html",
                {
                    "error": str(e),
                },
            )


class Add_set(View):
    def get(self, request, *args, **kwargs):

        campaign_id = request.GET.get("campaign_id")

        context_var = self.context(campaign_id)

        return render(request, "add_set.html", context_var)

    def context(self, campaign_id):

        return {
            "campaign_id": campaign_id,
        }

    def post(self, request, *args, **kwargs):

        access_token = (settings.USER_ACCESS_TOKEN)

        campaign_id = request.POST.get("campaign_id")
        bid_amount = request.POST.get("bid_amount")
        billing_event = request.POST.get("billing_event")
        daily_budget = request.POST.get("daily_budget")
        name = request.POST.get("name")
        optimization_goal = request.POST.get("optimization_goal")
        destination_type = request.POST.get("destination_type")
        page_id = request.POST.get("page_id")
        status = request.POST.get("status")

        data = {
            "access_token": access_token,
            "bid_amount": bid_amount,
            "billing_event": billing_event,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget,
            "name": name,
            "optimization_goal": optimization_goal,
            "destination_type": destination_type,
            "promoted_object": {"page_id": page_id},
            "status": status,
        }

        print("Ad Set Payload:")
        print(data)

        url = "https://graph.facebook.com/v26.0/act_4755523421433857/adsets"

        try:
            response = requests.post(
                url,
                data=data,
                timeout=30,
            )

            response_data = response.json()

            print("Meta Response:")
            print(response_data)

            if response.ok:
                return render(
                    request,
                    "add_set.html",
                    {
                        "campaign_id": campaign_id,
                        "success": "Ad Set created successfully.",
                        "meta_response": response_data,
                    },
                )

            return render(
                request,
                "add_set.html",
                {
                    "campaign_id": campaign_id,
                    "error": response_data,
                },
            )

        except requests.RequestException as e:
            return render(
                request,
                "add_set.html",
                {
                    "campaign_id": campaign_id,
                    "error": str(e),
                },
            )
