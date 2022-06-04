<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class MerchantSetting extends Model
{
    use HasFactory;

    protected $fillable = [
        'price_include_vat',
        "vat_percentage",
        "shipping_cost",
        "merchant_id",
    ];

    public function parent() {
        return $this->belongsTo(Merchant::class, "merchant_id");
    }

}
