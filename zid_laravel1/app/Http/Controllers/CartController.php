<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreCartRequest;
use App\Http\Requests\UpdateCartRequest;
use App\Http\Resources\CartResource;
use App\Models\Cart;
use App\Models\CartItem;
use App\Models\Customer;
use App\Models\Product;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

class CartController extends Controller
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
            "item" => "required|exists:products,id",
            "quantity" => "required|integer|min:0"
        ]);

        $product = Product::firstWhere("id", $request->item);
        if ($request->quantity > $product->inventory) {
            return ValidationException::withMessages(["quantity" => "Not enough inventory"]);
        }

        $customer = Customer::firstWhere("user_id", $request->user()->id);
        $cart = Cart::firstOrCreate(["customer_id" => $customer->id, "is_paid" => false]);
        $current = CartItem::firstWhere(["cart_id" => $cart->id, "item_id" => $product->id]);
        if ($current) {
            $current->quantity = $request->quantity;
            $current->save();
        } else {
            CartItem::create([
                "cart_id" => $cart->id,
                "item_id" => $product->id,
                "quantity" => $request->quantity,
            ]);
        }
        return response()->json(["details" => "Item Successfully added to cart!"]);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreCartRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreCartRequest $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Cart  $cart
     * @return CartResource
     */
    public function show(Request $request)
    {
        $customer = Customer::firstWhere("user_id", $request->user()->id);
        $cart = Cart::firstOrCreate(["customer_id" => $customer->id, "is_paid" => false]);
        return new CartResource($cart);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\Cart  $cart
     * @return \Illuminate\Http\Response
     */
    public function edit(Cart $cart)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateCartRequest  $request
     * @param  \App\Models\Cart  $cart
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateCartRequest $request, Cart $cart)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Cart  $cart
     * @return \Illuminate\Http\Response
     */
    public function destroy(Cart $cart)
    {
        //
    }
}
