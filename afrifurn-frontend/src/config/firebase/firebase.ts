import { getAuth } from 'firebase/auth';
import firebase from 'firebase/compat/app';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY||"AIzaSyAyWpBw5f__gaJngW40XlD7_fqbLS_Z6ns",
  authDomain: "auth-service-2409c.firebaseapp.com",
  projectId: "auth-service-2409c",
  storageBucket: "auth-service-2409c.appspot.com",
  messagingSenderId: "22779108741",
  appId: "1:22779108741:web:8b5bcbf942fd121ab0b8ec"
};

const app = firebase.initializeApp(firebaseConfig)

export const auth = getAuth(app);