<?php

namespace App\Http\Resources;

use App\Models\CartItem;
use App\Models\MerchantSetting;
use Illuminate\Http\Resources\Json\JsonResource;

class CartResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param \Illuminate\Http\Request $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request)
    {
        $items = CartItem::where("cart_id", $this->id)->get();
        $totals = 0;
        $total_no_vat = 0;
        $vat = 0;
        $shipping = 0;
        if ($items) {
            $merchant_id = $items[0]["item"]->merchant_id;
            $store_settings = MerchantSetting::firstOrCreate(
                ["merchant_id" => $merchant_id],
                [
                    'price_include_vat' => true,
                    "vat_percentage" => 0,
                    "shipping_cost" => 0
                ]
            );
            $shipping = $store_settings->shipping_cost;
            foreach ($items as $item) {
                $item_qty_total = $item['item']->price * $item["quantity"];
                if ($store_settings->price_include_vat) {
                    $current = $item_qty_total / 1.15;
                    $total_no_vat += $current;
                    $vat += $item_qty_total - $current;
                } else {
                    $total_no_vat += $item_qty_total;
                    $vat += $item_qty_total * ($store_settings->vat_percentage / 100);
                }
            }
        }
        return [
            'id' => $this->id,
            "items" => CartItemResource::collection($items),
            "totals" => [
                "total_no_vat" => $total_no_vat,
                "vat" => $vat,
                "shipping" => $shipping,
                "total" => $total_no_vat + $vat + $shipping
            ]
        ];
    }
}
