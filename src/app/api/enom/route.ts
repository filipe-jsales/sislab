import axios from "axios";

export default async function getData() {
  const response = axios.get(
    "https://resellertest.enom.com/interface.asp?command=check&sld=google&tld=com&uid=resellid&pw=resellpw"
  );
    console.log(response);
  return (await response).data;
}
