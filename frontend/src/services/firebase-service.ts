import { initializeApp, FirebaseApp } from "firebase/app";
import { FirebaseError } from "@firebase/util";
import {
  Auth,
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  User,
} from "firebase/auth";
import {
  getDatabase,
  DatabaseReference,
  ref,
  child,
  get,
} from "firebase/database";

export interface ILogin {
  user?: User;
  token?: string;
  expiration?: Date;
}

export class FirebaseService {
  private static firebaseConfig = {
    apiKey: "AIzaSyB_Zc8GYf-p8viTOvlfmgoAInZvVzRrFog",
    authDomain: "march-380306.firebaseapp.com",
    databaseURL: "https://march-380306-default-rtdb.firebaseio.com",
    projectId: "march-380306",
    storageBucket: "march-380306.appspot.com",
    messagingSenderId: "794331921108",
    appId: "1:794331921108:web:3284e90da6c61e553ed941",
  };
  private app: FirebaseApp;
  public auth: Auth;
  private db: DatabaseReference;
  private provider: GoogleAuthProvider;

  private static scopes = [
    "https://mail.google.com/",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
  ];

  constructor() {
    this.app = initializeApp(FirebaseService.firebaseConfig);
    this.auth = getAuth(this.app);
    this.db = ref(getDatabase(this.app));

    this.provider = new GoogleAuthProvider();
    for (const scope of FirebaseService.scopes) {
      this.provider.addScope(scope);
    }
  }

  public logout = async () => {
    await this.auth.signOut();
  };

  public login = async (cb: (auth: ILogin) => void) => {
    try {
      const result = await signInWithPopup(this.auth, this.provider);
      const credential = GoogleAuthProvider.credentialFromResult(result);
      if (!credential || !credential.accessToken) {
        throw new Error("Credential or token is null");
      }
      console.log("Logged In!", credential);
      const idTokenResult = await result.user.getIdTokenResult();
      console.log("IDToken Result", idTokenResult);
      const expiration = new Date(idTokenResult.expirationTime);
      console.log("Expiration", expiration);
      const token = credential.accessToken;
      cb({ user: result.user, token, expiration });
    } catch (error) {
      if (error instanceof FirebaseError) {
        console.error("Failed to loging.", error.code, error.message);
      } else {
        console.error(error);
      }
    }
  };

  public getConfigVariable = async (variable: string) => {
    let snapshot;
    try {
      snapshot = await get(child(this.db, `config/${variable}`));
    } catch (error) {
      console.error(error);
      throw new Error(`Variable ${variable} is not available`);
    }
    if (snapshot.exists()) {
      return snapshot.val();
    } else {
      throw new Error(`Variable ${variable} is not available`);
    }
  };
}
