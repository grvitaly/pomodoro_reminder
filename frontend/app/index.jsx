import { Redirect, useRouter, Stack } from "expo-router";
import { Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Index() {
  const router = useRouter();
  return (
    <SafeAreaView>
      <Text>Fignya, hernya</Text>
    </SafeAreaView>
  );
  // return <Redirect href="/home" />;
}
