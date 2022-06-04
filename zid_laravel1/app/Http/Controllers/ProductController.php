<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreProductRequest;
use App\Http\Requests\UpdateProductRequest;
use App\Models\Language;
use App\Models\Merchant;
use App\Models\Product;
use App\Models\ProductLangInfo;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class ProductController extends Controller
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
            "title" => "required|string",
            "description" => "present|string|nullable",
            "price" => "required|numeric|between:0,999999.99",
            "inventory" => "required|integer|min:0",
            "internationals" => "present|array",
            "internationals.*.language" => "required|exists:languages,abbreviation",
            "internationals.*.title" => "required|string",
            "internationals.*.description" => "present|string|nullable",
        ]);

        $user_id = $request->user()->id;

        $merchant = Merchant::firstWhere("user_id", $user_id);

        $product = Product::create([
            "title" => $request->title,
            "description" => $request->description,
            "price" => $request->price,
            "inventory" => $request->inventory,
            "merchant_id" => $merchant->id,
        ]);

        if ($request->internationals) {
            foreach ($request->internationals as $value) {
                Log::info(print_r($value, true));
                ProductLangInfo::create([
                    "product_id" => $product->id,
                    "language_id" => Language::firstWhere("abbreviation", $value['language'])->id,
                    "title" => $value['title'],
                    "description" => $value['description'],
                ]);
            }
        }
        return response()->json(["details" => "Product Successfully added!"]);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param \App\Http\Requests\StoreProductRequest $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreProductRequest $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param \App\Models\Product $product
     * @return \Illuminate\Http\Response
     */
    public function show(Product $product)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param \App\Models\Product $product
     * @return \Illuminate\Http\Response
     */
    public function edit(Product $product)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param \App\Http\Requests\UpdateProductRequest $request
     * @param \App\Models\Product $product
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateProductRequest $request, Product $product)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param \App\Models\Product $product
     * @return \Illuminate\Http\Response
     */
    public function destroy(Product $product)
    {
        //
    }
}
