import { GmailService } from "./gmail-service";
import * as firebase_service from "./firebase-service";
import nock from "nock";

jest.mock("./firebase-service.mjs");

describe("GmailService", () => {
  describe("search", () => {
    const mock_getConfigVariable = (firebase_service.getConfigVariable =
      jest.fn());
    const emails = [{ from: "test@test.com", to: "test2@test.com" }];
    it("should call firebase-service.getConfigVariable", async () => {
      mock_getConfigVariable.mockResolvedValue("http://127.0.0.1");
      const scope = nock("http://127.0.0.1")
        .get("/gmail/search")
        .reply(200, emails);
      const res = await GmailService.search("myquery", "myuser", "mytoken");
      expect(mock_getConfigVariable).toHaveBeenCalledTimes(1);
      expect(mock_getConfigVariable).toHaveBeenCalledWith("backend_url");
      expect(scope.isDone()).toBeTruthy();
      expect(res).toEqual(emails);
    });
  });
});
