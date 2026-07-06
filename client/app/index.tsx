import { api } from "@/convex/_generated/api";
import { useQuery } from "convex/react";
import { Text, View } from "react-native";

export default function Index() {
  const events = useQuery(api.events.get);
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {events?.map(({ _id, name }) => (
        <Text key={_id}>{name}</Text>
      ))}
    </View>
  );
}
