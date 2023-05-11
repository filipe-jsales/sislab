import CardDomain from "@/components/domains/card-domain";
import SearchDomain from "@/components/domains/search-domain";
import axios from "axios";

const getData = async () => {
  const response = axios.get("https://resellertest.enom.com/interface.asp?command=check&sld=google&tld=com&uid=resellid&pw=resellpw&");

  return (await response).data;
};

export default async function Home() {
  const response = await getData();

  console.log(response);
  return (
    <main className="flex min-h-screen min-w-full flex-col justify-between p-24">
      <SearchDomain/>
    </main>
  );
}
