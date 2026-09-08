function SearchBar({ search, onSearchChange }) {
  return (
    <input
      type="text"
      value={search}
      onChange={(event) => onSearchChange(event.target.value)}
      placeholder="Search recipes..."
      className="w-full rounded-xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-orange-500"
    />
  );
}

export default SearchBar;