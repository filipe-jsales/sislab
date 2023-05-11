"use client";
import React, { useState } from "react";
import CardDomain from "./card-domain";
import DomainAvailable from "./domain-available";

export default function SearchDomain() {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (event: any) => {
    setInputValue(event.target.value);
  };

  return (
    <div>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mt-2 flex rounded-md shadow-sm mb-10 w-4/12">
          <input
            type="text"
            name="company-website"
            id="company-website"
            className="block w-auto min-w-0 flex-1 rounded-none rounded-r-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-5 "
            placeholder="Search for domains"
            value={inputValue}
            onChange={handleInputChange}
          />
        </div>
      </div>
      <div>{inputValue && <DomainAvailable inputValue={inputValue} />}</div>
      <div>
        <CardDomain inputValue={inputValue} />
      </div>
    </div>
  );
}
