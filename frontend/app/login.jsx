import { useEffect, useState } from "react";
import { StyleSheet, Text, View, Button, Image, TouchableOpacity } from "react-native";
import * as WebBrowser from "expo-web-browser";

import { HandleGoogleLogin, GoogleUseAuthRequest, RemoveValueFromGoogleStore, GoogleSigninButton } from "../components/GoogleLogin";

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
        <View>
          <TouchableOpacity
            disabled={!request}
            onPress={() => {
              promptAsync();
            }}
          >
            <Image
              source={require("../assets/SignInWithGoogle.png")}
              style={styles.images}
            />
          </TouchableOpacity>
          <TouchableOpacity>
            <Image
              source={require("../assets/SignInWithFacebook.png")}
              style={styles.images}
            />
          </TouchableOpacity>
          <TouchableOpacity>
            <Image
              source={require("../assets/SignInWithGithub.png")}
              style={styles.images}
            />
          </TouchableOpacity>
          <TouchableOpacity>
            <Image
              source={require("../assets/SignInWithEmail.png")}
              style={styles.images}
            />
          </TouchableOpacity>
        </View>
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
  images: { width: 220, height: 43, margin: 10 },
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
