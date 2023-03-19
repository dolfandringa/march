import axios from "axios";
import { getConfigVariable } from "./firebase-service";
export const GmailService = {
  search: async (query, username, token) => {
    query = `X-GM-RAW "${query}"`;
    console.log("query", query);
    console.log("username", username);
    console.log("token", token);
    const backend_url = await getConfigVariable("backend_url");
    const res = await axios.get(`${backend_url}/mail/gmail/search`, {
      params: {
        username,
        query,
        token,
      },
    });
    console.log("res", res.data);
    return res.data;
  },
};
