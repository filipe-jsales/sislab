
export default function CardDomain({inputValue}: any) {
    return (
      <div className="border-b border-gray-200 pb-5 sm:flex sm:items-center sm:justify-between mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div>
          <span className="text-3xl font-semibold leading-6 text-gray-900">
            {inputValue + ".com" || "example.com"}
          </span>
        <div className="mt-2 mb-1">
          <span>$90</span>
          <span className="ml-4">$99</span>
        </div>
        <div>
          <span className="text-gray-400 text-xs">On first year*</span>
        </div>
        </div>
        <div className="mt-3 sm:ml-4 sm:mt-0">
          <label htmlFor="mobile-search-candidate" className="sr-only">
            Search
          </label>
          <label htmlFor="desktop-search-candidate" className="sr-only">
            Search
          </label>
          <div className="flex rounded-md shadow-sm">
            <button
              type="button"
              className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    );
  }
  