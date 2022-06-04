<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MerchantController;
use App\Http\Controllers\CustomerController;
use App\Http\Controllers\MerchantSettingController;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\CartController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post("/login", [AuthController::class, "login"]);
Route::post("/signup", [AuthController::class, "signup"]);

Route::prefix("merchant")->group(function () {
    Route::post("/register", [MerchantController::class, "create"]);
    Route::put("/update-info", [MerchantSettingController::class, "create"])->middleware(["auth:sanctum", "is.merchant"]);
    Route::post("/add-product", [ProductController::class, "create"])->middleware(["auth:sanctum", "is.merchant"]);
});

Route::prefix("customer")->group(function () {
    Route::post("/register", [CustomerController::class, "create"]);
    Route::post("/cart/add", [CartController::class, "create"])->middleware(["auth:sanctum", "is.customer"]);
    Route::get("/cart", [CartController::class, "show"])->middleware(["auth:sanctum", "is.customer"]);
});

