<?php

namespace App\Http\Resources;

use App\Models\ProductLangInfo;
use Illuminate\Http\Resources\Json\JsonResource;

class ProductResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request)
    {
        $internationals = ProductLangInfo::where("product_id", $this->id)->get();
        if ($internationals) {
            foreach ($internationals as $value) {
                $internationals_resp[] = [
                    "language" => $value["language"]->abbreviation,
                    "title" => $value["title"],
                    "description" => $value["description"]
                ];
            }
        }
        return [
            'id' => $this->id,
            "title" => $this->title,
            "description" => $this->description,
            "price" => $this->price,
            "inventory" => $this->inventory,
            "internationals" => $internationals_resp,
        ];
    }
}
