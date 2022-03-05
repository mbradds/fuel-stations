import { getRouteData } from "./modules/getRouteData";
import "./css/main.css";

async function main() {
  const data = await getRouteData("ELEC", "Calgary,ab", "London,on", 500, "CA");
  console.log(data);
}

main();
