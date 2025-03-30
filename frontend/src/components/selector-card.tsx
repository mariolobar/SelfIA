import { useAppContext } from "../core/context/AppContext";

interface SelectorCardProps {
  img: string;
  label: string;
  isSelected: boolean;
  onClick: (event: React.MouseEvent) => void;
}

export const SelectorCard: React.FC<SelectorCardProps> = ({
  img,
  label,
  isSelected,
  onClick,
}) => {
  const { filter } = useAppContext();

  return (
    <div
      className={`w-full max-w-80 rounded-3xl overflow-hidden shadow-md cursor-pointer ${
        isSelected ? "text-secondary outline outline-4 outline-secondary" : ""
      }`}
      onClick={onClick}
    >
      {!filter && (
        <div className="aspect-square overflow-hidden ">
          <img src={img} />
        </div>
      )}
      <p className="font-display text-5xl text-center py-4 px-8 bg-almost-white">
        {label}
      </p>
    </div>
  );
};

export default SelectorCard;
