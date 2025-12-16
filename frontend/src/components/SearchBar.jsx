function SearchBar({ value, onChange, onSubmit, placeholder }) {
  return (
    <div className="stack">
      <input
        className="input"
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSubmit()}
      />
      <div className="cta-row">
        <button className="btn" onClick={onSubmit}>
          Search
        </button>
        <span className="muted">Searches by title or keywords.</span>
      </div>
    </div>
  );
}

export default SearchBar;
