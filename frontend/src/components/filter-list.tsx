import { useAppContext } from "../core/context/AppContext";
import { Filter } from "../core/model/enum/filter.enum";
import SelectorCard from "./selector-card";

import MyPixar from "../assets/images/mypixar.png";
import FunkoMe from "../assets/images/funkome.png";
import SnapHero from "../assets/images/snaphero.png";

export const FilterList = () => {
  const { filter, setFilter } = useAppContext();

  return (
    <section
      className={`flex items-center p-6 ${
        filter ? "flex-col gap-6" : "flex-col lg:flex-row justify-center gap-16"
      }`}
    >
      <SelectorCard
        img={MyPixar}
        label="My Pixar"
        isSelected={filter === Filter.myPixar}
        onClick={() => setFilter(Filter.myPixar)}
      />
      <SelectorCard
        img={FunkoMe}
        label="Funko Me"
        isSelected={filter === Filter.funkoMe}
        onClick={() => setFilter(Filter.funkoMe)}
      />
      <SelectorCard
        img={SnapHero}
        label="Snap Hero"
        isSelected={filter === Filter.snapHero}
        onClick={() => setFilter(Filter.snapHero)}
      />
    </section>
  );
};

export default SelectorCard;
