import axios from "axios";
export class GmailService {
  static async search(
    backend_url: string,
    query: string,
    username: string,
    token: string
  ) {
    query = `X-GM-RAW "${query}"`;
    const res = await axios.get(`${backend_url}/mail/gmail/search`, {
      params: {
        username,
        query,
        token,
      },
    });
    return res.data;
  }
}
