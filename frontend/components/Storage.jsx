import AsyncStorage from "@react-native-async-storage/async-storage";

export async function RemoveValueFromStore(storeName) {
  await AsyncStorage.removeItem(storeName);
}

export async function ReadValueFromLocalStore(storeName) {
  const data = await AsyncStorage.getItem(storeName);
  if (!data) return null;
  const user = JSON.parse(data);
  return user;
}

export async function StoreValueToLocalStore(user, storeName) {
  await AsyncStorage.setItem(storeName, JSON.stringify(user));
}
