import * as Google from "expo-auth-session/providers/google";
import { ReadValueFromLocalStore, StoreValueToLocalStore, RemoveValueFromStore } from "./Storage";
import { ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID } from "./env";

const GOOGLE_USER_STORE_NAME = "@user-google";

export function GoogleUseAuthRequest() {
  return Google.useAuthRequest({
    androidClientId: ANDROID_CLIENT_ID,
    iosClientId: IOS_CLIENT_ID,
    webClientId: WEB_CLIENT_ID
  });
}

export async function RemoveValueFromGoogleStore() {
  await RemoveValueFromStore(GOOGLE_USER_STORE_NAME);
}

export async function LoadUserInformationFromGoogleByToken(token) {
  try {
    const response = await fetch("https://www.googleapis.com/userinfo/v2/me", {
      headers: { Authorization: `Bearer ${token}` }
    });
    const user = await response.json();
    return user;
  } catch (error) {
    return null;
  }
}

export async function HandleGoogleLogin(response) {
  const user = await ReadValueFromLocalStore(GOOGLE_USER_STORE_NAME);
  if (user) return user;

  if (response?.type === "success") {
    if (!response.authentication.accessToken) return;
    const user = await LoadUserInformationFromGoogleByToken(response.authentication.accessToken);
    StoreValueToLocalStore(user, GOOGLE_USER_STORE_NAME);
  }
  return user;
}
