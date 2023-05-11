
export default function CardDomain({inputValue}: any) {
    return (
      <div className="border-b border-gray-200 pb-5 sm:flex sm:items-center sm:justify-between">
        <div>
          <h3 className="text-base font-semibold leading-6 text-gray-900">
            {inputValue + ".com" || "example.com"}
          </h3>
        <div>
          <a href="teste">Desconto</a>
          <a className="ml-4" href="teste">Preço normal</a>
        </div>
        <div>
          <a className="text-xs" href="teste">On first year*</a>
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
  