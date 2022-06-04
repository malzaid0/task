<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    public function login(Request $request) {
        $login = $request->validate([
            "email" => "required|email",
            "password" => "required|string",
        ]);

        if (!Auth::attempt($login)) {
            return response(["details" => "Invalid email or password"]);
        }

        $token = Auth::user()->createToken('api_token')->plainTextToken;

        return response()->json(["token" => $token]);
    }

    public function signup(Request $request) {
        $request->validate([
//            "name" => "required|string",
            "email" => "required|email|unique:users",
            "password" => "required|string",
        ]);

        $user = User::create([
//            "name" => $request->name,
            "email" => $request->email,
            "password" => Hash::make($request->password),
        ]);

        $accessToken = $user->createToken('api_token')->plainTextToken;

        return response()->json(["token" => $accessToken]);
    }

}
