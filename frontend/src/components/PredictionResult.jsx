import React from 'react';
import styles from './PredictionResult.module.css';

export default function PredictionResult({ result, onReset }) {
  if (!result) return null;

  const { disease, recommendations } = result;
  const { precautions, medications, workout, diet } = recommendations;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.diseaseName}>
          <span className={styles.label}>Predicted Disease:</span>
          {disease}
        </h2>
        <button className={styles.resetButton} onClick={onReset}>
          Start Over
        </button>
      </div>

      <div className={styles.grid}>
        <div className={`${styles.card} ${styles.precautions}`}>
          <h3>🛡️ Precautions</h3>
          {precautions?.length > 0 ? (
            <ul>
              {precautions.map((p, i) => <li key={i}>{p}</li>)}
            </ul>
          ) : (
            <p className={styles.empty}>No precautions found.</p>
          )}
        </div>

        <div className={`${styles.card} ${styles.medications}`}>
          <h3>💊 Medications</h3>
          {medications?.length > 0 ? (
            <ul>
              {medications.map((m, i) => <li key={i}>{m}</li>)}
            </ul>
          ) : (
            <p className={styles.empty}>No medications found.</p>
          )}
        </div>

        <div className={`${styles.card} ${styles.workout}`}>
          <h3>🏃 Workout</h3>
          {workout?.length > 0 ? (
            <ul>
              {workout.map((w, i) => <li key={i}>{w}</li>)}
            </ul>
          ) : (
            <p className={styles.empty}>No workout found.</p>
          )}
        </div>

        <div className={`${styles.card} ${styles.diet}`}>
          <h3>🥗 Diet</h3>
          {diet?.length > 0 ? (
            <ul>
              {diet.map((d, i) => <li key={i}>{d}</li>)}
            </ul>
          ) : (
            <p className={styles.empty}>No diet found.</p>
          )}
        </div>
      </div>
    </div>
  );
}
