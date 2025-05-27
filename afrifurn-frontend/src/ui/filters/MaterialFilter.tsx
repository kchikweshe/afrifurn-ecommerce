import { Material } from '@/types';

const MaterialFilter = ({ materials, onFilterChange }: { materials: Material[], onFilterChange: Function }) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange(value ? [value] : []);
  };

  return (
    <select
      className="border rounded-lg px-3 py-2 text-base font-semibold"
      onChange={handleChange}
      defaultValue=""
    >
      <option value="">All Materials</option>
      {materials.map((material) => (
        <option key={material._id} value={material._id}>{material.name}</option>
      ))}
    </select>
  );
};

export default MaterialFilter; 