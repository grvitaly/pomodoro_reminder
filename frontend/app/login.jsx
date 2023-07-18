import { useEffect, useState } from "react";
import { StyleSheet, Text, View, Button, Image } from "react-native";
import * as WebBrowser from "expo-web-browser";

import { HandleGoogleLogin, GoogleUseAuthRequest, RemoveValueFromGoogleStore } from "../components/GoogleLogin";

WebBrowser.maybeCompleteAuthSession();

export default function App() {
  const [userInfo, setUserInfo] = useState(null);

  const [request, response, promptAsync] = GoogleUseAuthRequest();

  useEffect(() => {
    handleEffect();
  }, [response]);

  async function handleEffect() {
    const user = await HandleGoogleLogin(response);
    setUserInfo(user);
  }

  return (
    <View style={styles.container}>
      {!userInfo ? (
        <Button
          title="Sign in with Google"
          disabled={!request}
          onPress={() => {
            promptAsync();
          }}
        />
      ) : (
        <View style={styles.card}>
          {userInfo?.picture && (
            <Image
              source={{ uri: userInfo?.picture }}
              style={styles.image}
            />
          )}
          <Text style={styles.text}>Email: {userInfo.email}</Text>
          <Text style={styles.text}>Verified: {userInfo.verified_email ? "yes" : "no"}</Text>
          <Text style={styles.text}>Name: {userInfo.name}</Text>
          {/* <Text style={styles.text}>{JSON.stringify(userInfo, null, 2)}</Text> */}
        </View>
      )}
      <Button
        title="remove local store"
        onPress={RemoveValueFromGoogleStore}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  },
  text: {
    fontSize: 20,
    fontWeight: "bold"
  },
  card: {
    borderWidth: 1,
    borderRadius: 15,
    padding: 15
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 50
  }
});
