import { useState, useRef, useEffect } from "react";
import styles from "./SymptomSelector.module.css";

export default function SymptomSelector({ features, selected, onChange }) {
  const [search, setSearch] = useState("");
  const [focused, setFocused] = useState(false);
  const inputRef = useRef(null);

  const normalized = (s) => s.toLowerCase().replace(/_/g, " ");

  const filtered = features.filter((f) =>
    normalized(f).includes(search.toLowerCase())
  );

  const toggle = (symptom) => {
    const next = selected.includes(symptom)
      ? selected.filter((s) => s !== symptom)
      : [...selected, symptom];
    onChange(next);
  };

  const clearAll = () => onChange([]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.topBar}>
        <div className={styles.searchBox}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            ref={inputRef}
            type="text"
            placeholder="Search symptoms…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setTimeout(() => setFocused(false), 150)}
            className={styles.searchInput}
            id="symptom-search"
          />
          {search && (
            <button className={styles.clearSearch} onClick={() => setSearch("")}>
              ✕
            </button>
          )}
        </div>
        <div className={styles.countBadge}>
          {selected.length} selected
          {selected.length > 0 && (
            <button className={styles.clearAll} onClick={clearAll}>
              Clear all
            </button>
          )}
        </div>
      </div>

      {/* Selected tags */}
      {selected.length > 0 && (
        <div className={styles.tagStrip}>
          {selected.map((s) => (
            <span key={s} className={styles.tag} onClick={() => toggle(s)}>
              {normalized(s)} ✕
            </span>
          ))}
        </div>
      )}

      {/* Grid */}
      <div className={styles.grid}>
        {filtered.length === 0 ? (
          <p className={styles.noResults}>No symptoms match "{search}"</p>
        ) : (
          filtered.map((f) => {
            const isSelected = selected.includes(f);
            return (
              <label
                key={f}
                className={`${styles.item} ${isSelected ? styles.checked : ""}`}
              >
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => toggle(f)}
                  className={styles.checkbox}
                  id={`symptom-${f}`}
                />
                <span className={styles.symptomName}>{normalized(f)}</span>
              </label>
            );
          })
        )}
      </div>
    </div>
  );
}
