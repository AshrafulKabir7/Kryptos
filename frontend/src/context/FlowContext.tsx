import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';

export type FlowStep = {
  label: string;
  detail?: string;
  status: 'pending' | 'active' | 'done';
};

export type FlowState = {
  active: boolean;
  title: string;
  direction: 'encrypt' | 'decrypt';
  algorithm: string;
  steps: FlowStep[];
};

type FlowContextType = {
  flow: FlowState;
  triggerFlow: (algorithm: string, direction: 'encrypt' | 'decrypt') => void;
  clearFlow: () => void;
};

const defaultFlow: FlowState = {
  active: false,
  title: '',
  direction: 'encrypt',
  algorithm: '',
  steps: [],
};

const FlowContext = createContext<FlowContextType>({
  flow: defaultFlow,
  triggerFlow: () => {},
  clearFlow: () => {},
});

export const useFlow = () => useContext(FlowContext);

// Predefined cryptographic flows
const FLOWS: Record<string, Record<string, FlowStep[]>> = {
  substitution: {
    encrypt: [
      { label: 'Plaintext Input', detail: 'Raw ASCII buffer received', status: 'pending' },
      { label: 'Key Validation', detail: 'Verify 26-char bijective map', status: 'pending' },
      { label: 'Character Mapping', detail: 'A→K, B→Q, C→D ...', status: 'pending' },
      { label: 'Sequential Substitution', detail: 'Apply map to each character', status: 'pending' },
      { label: 'Frequency Analysis', detail: 'Count character distribution', status: 'pending' },
      { label: 'Ciphertext Output', detail: 'Encrypted payload ready', status: 'pending' },
    ],
    decrypt: [
      { label: 'Ciphertext Input', detail: 'Encrypted buffer received', status: 'pending' },
      { label: 'Inverse Key Generation', detail: 'Reverse the substitution map', status: 'pending' },
      { label: 'Reverse Mapping', detail: 'K→A, Q→B, D→C ...', status: 'pending' },
      { label: 'Sequential Reversal', detail: 'Apply inverse map per char', status: 'pending' },
      { label: 'Plaintext Output', detail: 'Decrypted payload recovered', status: 'pending' },
    ],
  },
  transposition: {
    encrypt: [
      { label: 'Plaintext Input', detail: 'Raw text buffer', status: 'pending' },
      { label: 'Keyword → Permutation', detail: 'Convert keywords to column order', status: 'pending' },
      { label: 'First Grid Write', detail: 'Fill row-major matrix', status: 'pending' },
      { label: 'Column Permutation #1', detail: 'Reorder columns by Key 1', status: 'pending' },
      { label: 'Second Grid Write', detail: 'Re-fill with intermediate text', status: 'pending' },
      { label: 'Column Permutation #2', detail: 'Reorder columns by Key 2', status: 'pending' },
      { label: 'Ciphertext Output', detail: 'Read columns sequentially', status: 'pending' },
    ],
    decrypt: [
      { label: 'Ciphertext Input', detail: 'Scrambled buffer received', status: 'pending' },
      { label: 'Inverse Permutation #2', detail: 'Reverse Key 2 column order', status: 'pending' },
      { label: 'Grid Reconstruction', detail: 'Reform intermediate matrix', status: 'pending' },
      { label: 'Inverse Permutation #1', detail: 'Reverse Key 1 column order', status: 'pending' },
      { label: 'Row-major Read', detail: 'Read original row order', status: 'pending' },
      { label: 'Plaintext Output', detail: 'Decrypted text recovered', status: 'pending' },
    ],
  },
  aes: {
    encrypt: [
      { label: 'Plaintext Input', detail: 'UTF-8 → 128-bit blocks', status: 'pending' },
      { label: 'Key Generation', detail: 'Random 128-bit secret key', status: 'pending' },
      { label: 'Key Expansion', detail: 'Generate 11 round keys', status: 'pending' },
      { label: 'Initial AddRoundKey', detail: 'XOR state with Round Key 0', status: 'pending' },
      { label: 'SubBytes', detail: 'S-Box non-linear substitution', status: 'pending' },
      { label: 'ShiftRows', detail: 'Cyclic byte shifting', status: 'pending' },
      { label: 'MixColumns', detail: 'GF(2⁸) matrix multiplication', status: 'pending' },
      { label: 'AddRoundKey', detail: 'XOR with round key (×9 rounds)', status: 'pending' },
      { label: 'Final Round', detail: 'SubBytes → ShiftRows → AddRoundKey', status: 'pending' },
      { label: 'Ciphertext Output', detail: 'Hex-encoded block ready', status: 'pending' },
    ],
    decrypt: [
      { label: 'Ciphertext Input', detail: 'Hex block + key received', status: 'pending' },
      { label: 'Key Expansion', detail: 'Regenerate 11 round keys', status: 'pending' },
      { label: 'Initial AddRoundKey', detail: 'XOR state with Round Key 10', status: 'pending' },
      { label: 'InvShiftRows', detail: 'Reverse cyclic shifting', status: 'pending' },
      { label: 'InvSubBytes', detail: 'Inverse S-Box lookup', status: 'pending' },
      { label: 'InvMixColumns', detail: 'Inverse GF(2⁸) multiply', status: 'pending' },
      { label: 'AddRoundKey', detail: 'XOR with round key (×9)', status: 'pending' },
      { label: 'Final Inverse Round', detail: 'InvShiftRows → InvSubBytes → AddRoundKey', status: 'pending' },
      { label: 'Plaintext Output', detail: 'UTF-8 text recovered', status: 'pending' },
    ],
  },
  des: {
    encrypt: [
      { label: 'Plaintext Input', detail: 'UTF-8 → 64-bit blocks', status: 'pending' },
      { label: 'Key Generation', detail: 'Random 64-bit key (56 effective)', status: 'pending' },
      { label: 'Initial Permutation', detail: 'IP bit rearrangement', status: 'pending' },
      { label: 'Key Schedule', detail: 'Generate 16 × 48-bit subkeys', status: 'pending' },
      { label: 'Feistel Round ×16', detail: 'Expand → XOR → S-Box → P-Box', status: 'pending' },
      { label: 'L/R Swap', detail: 'Final halves swap', status: 'pending' },
      { label: 'Final Permutation', detail: 'IP⁻¹ bit rearrangement', status: 'pending' },
      { label: 'Ciphertext Output', detail: 'Hex-encoded 64-bit block', status: 'pending' },
    ],
    decrypt: [
      { label: 'Ciphertext Input', detail: 'Hex block + key received', status: 'pending' },
      { label: 'Initial Permutation', detail: 'IP bit rearrangement', status: 'pending' },
      { label: 'Key Schedule (Reversed)', detail: 'Subkeys applied in reverse', status: 'pending' },
      { label: 'Feistel Round ×16', detail: 'Expand → XOR → S-Box → P-Box', status: 'pending' },
      { label: 'L/R Swap', detail: 'Final halves swap', status: 'pending' },
      { label: 'Final Permutation', detail: 'IP⁻¹ output', status: 'pending' },
      { label: 'Plaintext Output', detail: 'UTF-8 text recovered', status: 'pending' },
    ],
  },
  rsa: {
    encrypt: [
      { label: 'Plaintext Input', detail: 'Text → integer encoding', status: 'pending' },
      { label: 'Load Public Key', detail: 'Read (n, e) pair', status: 'pending' },
      { label: 'Modular Exponentiation', detail: 'c = m^e mod n', status: 'pending' },
      { label: 'Ciphertext Output', detail: 'Big integer ciphertext', status: 'pending' },
    ],
    decrypt: [
      { label: 'Ciphertext Input', detail: 'Big integer received', status: 'pending' },
      { label: 'Load Private Key', detail: 'Read (n, d) pair', status: 'pending' },
      { label: 'Modular Exponentiation', detail: 'm = c^d mod n', status: 'pending' },
      { label: 'Integer → Text', detail: 'Decode to UTF-8', status: 'pending' },
      { label: 'Plaintext Output', detail: 'Original message recovered', status: 'pending' },
    ],
  },
  rsa_keygen: {
    encrypt: [
      { label: 'Prime Generation', detail: 'Find large primes p, q', status: 'pending' },
      { label: 'Compute n = p × q', detail: 'RSA modulus', status: 'pending' },
      { label: 'Euler Totient', detail: 'φ(n) = (p-1)(q-1)', status: 'pending' },
      { label: 'Choose e', detail: 'Public exponent (65537)', status: 'pending' },
      { label: 'Compute d', detail: 'd = e⁻¹ mod φ(n)', status: 'pending' },
      { label: 'Keys Ready', detail: 'Public (n,e) + Private (n,d)', status: 'pending' },
    ],
    decrypt: [
      { label: 'Prime Generation', detail: 'Find large primes p, q', status: 'pending' },
      { label: 'Compute n = p × q', detail: 'RSA modulus', status: 'pending' },
      { label: 'Euler Totient', detail: 'φ(n) = (p-1)(q-1)', status: 'pending' },
      { label: 'Choose e', detail: 'Public exponent (65537)', status: 'pending' },
      { label: 'Compute d', detail: 'd = e⁻¹ mod φ(n)', status: 'pending' },
      { label: 'Keys Ready', detail: 'Public (n,e) + Private (n,d)', status: 'pending' },
    ],
  },
  ecdh: {
    encrypt: [
      { label: 'Select Curve', detail: 'Load (p, a, b, G, n) params', status: 'pending' },
      { label: 'Node A: Private Key', detail: 'Random scalar dₐ ∈ [1, n-1]', status: 'pending' },
      { label: 'Node A: Public Key', detail: 'Qₐ = dₐ · G (point multiply)', status: 'pending' },
      { label: 'Node B: Private Key', detail: 'Random scalar d_b ∈ [1, n-1]', status: 'pending' },
      { label: 'Node B: Public Key', detail: 'Q_b = d_b · G', status: 'pending' },
      { label: 'Exchange Public Keys', detail: 'Qₐ ↔ Q_b over insecure channel', status: 'pending' },
      { label: 'Compute Shared Secret', detail: 'S = dₐ · Q_b = d_b · Qₐ', status: 'pending' },
      { label: 'Shared Key Ready', detail: 'Identical point on both sides', status: 'pending' },
    ],
    decrypt: [
      { label: 'Select Curve', detail: 'Load (p, a, b, G, n) params', status: 'pending' },
      { label: 'Node A: Private Key', detail: 'Random scalar dₐ ∈ [1, n-1]', status: 'pending' },
      { label: 'Node A: Public Key', detail: 'Qₐ = dₐ · G (point multiply)', status: 'pending' },
      { label: 'Node B: Private Key', detail: 'Random scalar d_b ∈ [1, n-1]', status: 'pending' },
      { label: 'Node B: Public Key', detail: 'Q_b = d_b · G', status: 'pending' },
      { label: 'Exchange Public Keys', detail: 'Qₐ ↔ Q_b over insecure channel', status: 'pending' },
      { label: 'Compute Shared Secret', detail: 'S = dₐ · Q_b = d_b · Qₐ', status: 'pending' },
      { label: 'Shared Key Ready', detail: 'Identical point on both sides', status: 'pending' },
    ],
  },
};

export function FlowProvider({ children }: { children: ReactNode }) {
  const [flow, setFlow] = useState<FlowState>(defaultFlow);

  const triggerFlow = (algorithm: string, direction: 'encrypt' | 'decrypt') => {
    const flowDef = FLOWS[algorithm]?.[direction];
    if (!flowDef) return;

    const steps = flowDef.map(s => ({ ...s, status: 'pending' as const }));
    const title = `${algorithm.toUpperCase()} ${direction === 'encrypt' ? 'Encryption' : 'Decryption'}`;

    setFlow({ active: true, title, direction, algorithm, steps });

    // Animate steps one by one
    steps.forEach((_, i) => {
      setTimeout(() => {
        setFlow(prev => ({
          ...prev,
          steps: prev.steps.map((s, j) => ({
            ...s,
            status: j < i ? 'done' : j === i ? 'active' : 'pending',
          })),
        }));
      }, 400 + i * 350);

      // Mark last as done
      if (i === steps.length - 1) {
        setTimeout(() => {
          setFlow(prev => ({
            ...prev,
            steps: prev.steps.map(s => ({ ...s, status: 'done' as const })),
          }));
        }, 400 + (i + 1) * 350);
      }
    });
  };

  const clearFlow = () => setFlow(defaultFlow);

  return (
    <FlowContext.Provider value={{ flow, triggerFlow, clearFlow }}>
      {children}
    </FlowContext.Provider>
  );
}
