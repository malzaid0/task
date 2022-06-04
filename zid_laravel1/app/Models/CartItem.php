<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class CartItem extends Model
{
    use HasFactory;

    protected $fillable = [
        "cart_id",
        "item_id",
        "quantity",
        "price_at_checkout"
    ];

    public function cart() {
        return $this->belongsTo(Cart::class, "cart_id");
    }

    public function item() {
        return $this->belongsTo(Product::class, "item_id");
    }

}
