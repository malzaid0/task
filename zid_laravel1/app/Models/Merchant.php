<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Merchant extends Model
{
    use HasFactory;

    protected $fillable = [
        'store_name',
        "user_id",
    ];

    public function parent() {
        return $this->belongsTo(User::class, "user_id");
    }
}
