<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreMerchantSettingRequest;
use App\Http\Requests\UpdateMerchantSettingRequest;
use App\Models\Merchant;
use App\Models\MerchantSetting;
use Illuminate\Http\Request;

class MerchantSettingController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function create(Request $request)
    {
        $request->validate([
            "store_name" => "string|required",
            "price_include_vat" => "boolean|required",
            "vat_percentage" => "required|integer|min:0",
            "shipping_cost" => "required|numeric|between:0,99999.99"
        ]);

        $user_id = $request->user()->id;

        $merchant = Merchant::firstWhere("user_id", $user_id);
        $merchant->store_name = $request->store_name;
        $merchant->save();

        $settings = MerchantSetting::firstWhere("merchant_is", $merchant->id);

        if ($settings) {
            $settings->price_include_vat = $request->price_include_vat;
            $settings->vat_percentage = $request->vat_percentage;
            $settings->shipping_cost = $request->shipping_cost;
        } else {
            MerchantSetting::create([
                "price_include_vat" => $request->price_include_vat,
                "vat_percentage" => $request->vat_percentage,
                "shipping_cost" => $request->shipping_cost,
                "merchant_id" => $merchant->id
            ]);
        }

        return response()->json(["details" => "Successfully updated"]);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreMerchantSettingRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreMerchantSettingRequest $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\MerchantSetting  $merchantSetting
     * @return \Illuminate\Http\Response
     */
    public function show(MerchantSetting $merchantSetting)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\MerchantSetting  $merchantSetting
     * @return \Illuminate\Http\Response
     */
    public function edit(MerchantSetting $merchantSetting)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateMerchantSettingRequest  $request
     * @param  \App\Models\MerchantSetting  $merchantSetting
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateMerchantSettingRequest $request, MerchantSetting $merchantSetting)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\MerchantSetting  $merchantSetting
     * @return \Illuminate\Http\Response
     */
    public function destroy(MerchantSetting $merchantSetting)
    {
        //
    }
}
