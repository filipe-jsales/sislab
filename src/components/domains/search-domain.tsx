"use client";
import React, { useState } from "react";
import CardDomain from "./card-domain";

export default function SearchDomain() {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (event: any) => {
    setInputValue(event.target.value);
  };

  return (
    <div>
      <div>
        <div className="mt-2 flex rounded-md shadow-sm mb-10 w-4/12">
          <span className="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 px-3 text-gray-500 sm:text-sm">
            https://www.
          </span>
          <input
            type="text"
            name="company-website"
            id="company-website"
            className="block w-auto min-w-0 flex-1 rounded-none rounded-r-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            placeholder=" example.com"
            value={inputValue}
            onChange={handleInputChange}
          />
        </div>
      </div>

      <div>
        <CardDomain inputValue={inputValue} />
      </div>
    </div>
  );
}
