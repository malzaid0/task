<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Cart extends Model
{
    use HasFactory;

    protected $fillable = [
        "is_paid",
        "customer_id",
    ];

    public function parent() {
        return $this->belongsTo(Customer::class, "customer_id");
    }

}
