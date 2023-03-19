import { initializeApp } from "firebase/app";
import {
  getAuth,
  signInWithPopup,
  onAuthStateChanged,
  GoogleAuthProvider,
} from "firebase/auth";
import { getDatabase, ref, child, get } from "firebase/database";

const firebaseConfig = {
  apiKey: "AIzaSyB_Zc8GYf-p8viTOvlfmgoAInZvVzRrFog",
  authDomain: "march-380306.firebaseapp.com",
  databaseURL: "https://march-380306-default-rtdb.firebaseio.com",
  projectId: "march-380306",
  storageBucket: "march-380306.appspot.com",
  messagingSenderId: "794331921108",
  appId: "1:794331921108:web:3284e90da6c61e553ed941",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = ref(getDatabase(app));

export const onAuthStateChange = (cb) => {
  return onAuthStateChanged(auth, async (user) => {
    if (user) {
      console.log("logged in!", user, auth);
      try {
        cb({ user: user });
      } catch (error) {
        console.error(error);
      }
    } else {
      cb(null);
      console.log("Not logged in.");
    }
  });
};

export const logout = async () => {
  await auth.signOut();
};

export const login = async (cb) => {
  const provider = new GoogleAuthProvider();
  const scopes = [
    "https://mail.google.com/",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
  ];
  for (const scope of scopes) {
    provider.addScope(scope);
  }
  try {
    const result = await signInWithPopup(auth, provider);
    const credential = GoogleAuthProvider.credentialFromResult(result);
    console.log("Logged In!", credential);
    const token = credential.accessToken;
    cb({ user: result.user, token });
  } catch (error) {
    console.error("Failed to loging.", error.code, error.message);
  }
};

export const getConfigVariable = async (variable) => {
  let snapshot;
  try {
    snapshot = await get(child(db, `config/${variable}`));
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
