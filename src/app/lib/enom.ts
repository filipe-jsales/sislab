//fetch enom util para fazer o request
//pegar o input e retornar a lista de dominios



//check domain availability 
// https://resellertest.enom.com/interface.asp?command=check&sld=google&tld=com&uid=resellid&pw=resellpw&responsetype=xml





/**
 * const getData = async () => {
  try {
    const response = await axios.get('https://resellertest.enom.com/interface.asp', {
      params: {
        command: 'check',
        sld: 'google',
        tld: 'com',
        uid: 'resellid',
        pw: 'resellpw',
        responsetype: 'xml'
      }
    });
    console.log(response.data);
  return  response.data;

  } catch (error) {
    console.error(error);
  }

};
 */



// import axios from 'axios';

// const makePurchaseRequest = async (endUserIP: string, sld: string, tld: string) => {
//   const apiKey = process.env.ENOM_API_DEVELOPMENT_KEY;
//   const url = `https://resellertest.enom.com/interface.asp?command=Purchase&uid=greenmainframe&pw=${apiKey}&EndUserIP=${endUserIP}&SLD=${sld}&TLD=${tld}&responsetype=xml`;

//   try {
//     const response = await axios.get(url);
//     return response.data;
//   } catch (error) {
//     console.error(error);
//     return null;
//   }
// };
