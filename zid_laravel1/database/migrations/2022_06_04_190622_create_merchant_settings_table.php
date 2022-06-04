<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('merchant_settings', function (Blueprint $table) {
            $table->id();
            $table->foreignId("merchant_id");
            $table->boolean("price_include_vat");
            $table->integer("vat_percentage")->nullable(true);
            $table->decimal("shipping_cost", $precision = 8, $scale = 2)->nullable(true);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('merchant_settings');
    }
};
