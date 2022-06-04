<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductLangInfo extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        "description",
        "product_id",
        "language_id",
    ];

    public function product() {
        return $this->belongsTo(Product::class, "product_id");
    }

    public function language() {
        return $this->belongsTo(Language::class, "language_id");
    }

}
