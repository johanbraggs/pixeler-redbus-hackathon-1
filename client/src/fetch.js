import axios from "axios";

const fetchFunc = async (url, method) => {
    try {
        let headersList = {
            "Accept": "*/*"
        }

        let reqOptions = {
            url: url,
            method: method,
            headers: headersList,
        }
        let response = await axios.request(reqOptions);
        console.log("response from fun", response.data);

        return response.data;

    } catch (error) {
        console.log(error)
    }
}

export {fetchFunc}