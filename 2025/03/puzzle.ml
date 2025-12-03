
let open_input (input_f: string option) : string list =
  let real_name = match input_f with
  | Some s -> s
  | None -> "input"
  in
  let input_channel = open_in real_name in
  let input_contents =
    really_input_string input_channel (in_channel_length input_channel) in
  close_in input_channel;
  String.split_on_char '\n' input_contents


(* Parses the input into a list of lists of joltages *)
let parse_input (input: string list) : int list list =
  List.filter_map (
    fun s -> if s="" then None
             else Some(List.map (fun c -> int_of_char c - 0x30) (List.of_seq (String.to_seq s)))
  ) input


let rec best_joltage_first_digit (first_digit: int) (max_acc: int)
    (current_rack: int list) : int =
  match current_rack with
  | [] -> max_acc
  | x::q ->
      best_joltage_first_digit first_digit (max max_acc (10*first_digit+x)) q


let rec best_joltages_first_digits (max_acc: int) (rack: int list) : int =
  match rack with
  | []
  | [_] -> max_acc
  | x::q ->
      best_joltages_first_digits (best_joltage_first_digit x max_acc q) q


let best_joltage (acc: int) (rack: int list) : int =
  acc + best_joltages_first_digits 0 rack

(* Solves part 1 *)
let solve_part1 (input: int list list) : int =
  List.fold_left best_joltage 0 input


(* Changement de stratégie : on regarde s’il y a un 9 qu’on peut placer au
 * début, puis un 8, etc., on le prend puis on cherche un deuxième chiffre, etc.
 *)
type resultat =
  | MeilleurNombre of int * int list
  | ChercherSurNmoins1

let rec premier_chiffre (rack: int list) (nombre_de_chiffres_restant: int)
    (chiffre_actuel: int) : resultat  =
  if List.length rack < nombre_de_chiffres_restant then ChercherSurNmoins1
  else
  match rack with
  | [] -> ChercherSurNmoins1
  | x::q when x = chiffre_actuel -> MeilleurNombre (chiffre_actuel, q)
  | x::q -> premier_chiffre q nombre_de_chiffres_restant chiffre_actuel


let rec meilleur (current: int) (rack: int list) (nombre_chiffres_restant: int)
    (chiffre: int): int =
  if nombre_chiffres_restant = 0 then current else
  if chiffre = 0 then assert false else
  match (premier_chiffre rack nombre_chiffres_restant chiffre) with
  | ChercherSurNmoins1 ->
      meilleur current rack nombre_chiffres_restant (chiffre-1)
  | MeilleurNombre (i, q) ->
      meilleur (current*10 + i) q (nombre_chiffres_restant-1) 9


let best_joltage2 (acc: int) (rack: int list) : int =
  acc + meilleur 0 rack 12 9

(* Solves part 2 *)
let solve_part2 (input: int list list) : int =
  snd (List.fold_left (fun (n, m) r -> print_int n; print_newline (); (n+1), (best_joltage2 m r)) (0, 0) input)

let solve (filename: string) =
  let input = parse_input (open_input (Some filename)) in
  print_int (solve_part1 input);
  print_newline ();
  print_int (solve_part2 input);
  print_newline ()
