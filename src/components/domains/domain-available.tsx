import styles from "./Domain.module.scss";

const tiers = [
  {
    name: "Your domain is available!",
    href: "#",
    discountPrice: 80,
    normalPrice: 88.9,
  },
  {
    name: "Popular in Brazil",
    href: "#",
    discountPrice: 99,
    normalPrice: 119,
  },
];

export default function DomainAvailable({inputValue}: any) {
  return (
    <div>
      <div className="mt-8 pb-12 sm:mt-12 sm:pb-16 lg:mt-16 lg:pb-24">
        <div className="relative">
          <div className="absolute inset-0 h-3/4 " />
          <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-md space-y-4 lg:grid lg:max-w-5xl lg:grid-cols-2 lg:gap-5 lg:space-y-0">
              {tiers.map((tier) => (
                <div
                  key={tier.name}
                  className="flex flex-col overflow-hidden rounded-lg shadow-lg"
                >
                  <div className="bg-white w-11/12">
                    <div className="bg-white px-6 py-8 sm:p-10 sm:pb-6">
                      <div className="border-b border-gray-200 pb-4">
                        <h3
                          className={styles.featured__h3}
                          id="tier-standard"
                        >
                          {tier.name}
                        </h3>
                      </div>
                      <div className="mt-4 flex items-baseline font-bold tracking-tight">
                        <span className="text-3xl">
                          {tier.name === "Popular in Brazil" ? inputValue + ".com.br" : inputValue + ".com" }
                        </span>
                      </div>
                      <div className="flex">
                        <p className="mt-5 mr-4 text-lg ">
                          ${tier.discountPrice}
                        </p>
                        <p className="mt-5 text-lg text-gray-500 line-through bg-gray-50">
                          ${tier.normalPrice}
                        </p>
                      </div>
                      <button
                        type="button"
                        className="rounded-full bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 mt-6"
                      >
                        Add to Cart
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="relative mx-auto mt-4 max-w-7xl px-4 sm:px-6 lg:mt-5 lg:px-8">
          <div className="mx-auto max-w-md lg:max-w-5xl"></div>
        </div>
      </div>
    </div>
  );
}
