import * as Google from "expo-auth-session/providers/google";
import { ReadValueFromLocalStore, StoreValueToLocalStore, RemoveValueFromStore } from "./Storage";

const GOOGLE_USER_STORE_NAME = "@user-google";

export function GoogleUseAuthRequest() {
  return Google.useAuthRequest({
    androidClientId: "458305486199-67l4l9g9o5mhkgeke7b037vq8ch3ph69.apps.googleusercontent.com",
    iosClientId: "458305486199-82cemvg2r8mj5nrunku5lsa1e73hmc0k.apps.googleusercontent.com",
    webClientId: "458305486199-v4b0odt50j7rs1f9jb3tb1p9j35grnv8.apps.googleusercontent.com"
  });
  // web secret: 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
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
