# RSA-PSI
Implementation of Private Set Intersection protocol based on RSA blind signature

# RSA-based Private Set Intersection

## Server side:

Let  $S = \{ s_1, s_2, \dots, s_w \}$

Compute hashed set:  
$S' = \{ h_{s_1}, h_{s_2}, \dots, h_{s_w} \}$, where $h_{s_i} = H(s_i)$

For each element:
- $K_{s_i} = (h_{s_i})^d \bmod n$
- $t_i = H'(K_{s_i})$

Server stores:  $\{ t_1, t_2, \dots, t_w \}$

Server receives:  $\{ y_1, y_2, \dots, y_v \}$

Compute:
$y'_i = (y_i)^d \bmod n$

Server sends:  $\{ y'_1, \dots, y'_v \}$ and $\{ t_1, \dots, t_w \}$

---

## Client side:

Let  $C = \{ c_1, c_2, \dots, c_v \}$

Compute:  $C' = \{ h_{c_1}, h_{c_2}, \dots, h_{c_v} \}$, where $h_{c_i} = H(c_i)$

For each $i$, choose  $R_i \xleftarrow{R} \mathbb{Z}_n^*$

Compute:
$y_i = h_{c_i} \cdot (R_i)^e \bmod n$

Client sends:  $\{ y_1, y_2, \dots, y_v \}$

After receiving $y'_i$:
- $K_{c_i} = y'_i \cdot R_i^{-1} \bmod n$
- ${t_{i}^{,}}$ = $H'(K_{c_i} )$

Output:
{ $t'_1, \dots, t'_v$ } $\cap$ { $t_1, \dots, t_w$ }
