import { Redirect } from "expo-router";
import { Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Index() {
  return (
    <SafeAreaView>
      <Text>Test</Text>
    </SafeAreaView>
  );
  // return <Redirect href="/home" />;
}