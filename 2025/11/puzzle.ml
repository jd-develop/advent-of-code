
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


let parse_input (input : string list) : (string * string list) list =
  List.filter_map
  (
    fun s ->
      if s = "" then None else
      let label, neighbours =
        match (String.split_on_char ':' s) with
        | [a; b] -> a, b
        | _ -> failwith "Erreur de syntaxe"
        in
      let n_split = String.split_on_char ' ' neighbours |> List.tl in
      Some(label, n_split)
  )
  input


let solve_part_1 (graph: (string * string list) list) (depart: string) =
  let rec explore_depuis (accu: int) (s: string) : int =
    if s = "out" then
      accu+1
    else
      List.fold_left explore_depuis accu (List.assoc s graph)
  in
  explore_depuis 0 depart


let fst5 (a, _, _, _, _) = a
let snd5 (_, a, _, _, _) = a
let thrd5 (_, _, a, _, _) = a
let frth5 (_, _, _, a, _) = a
let ffth5 (_, _, _, _, a) = a


let solve_part_2 (graph: (string * string list) list) =
  let rec explore_depuis (seen_fft: bool) (seen_dac: bool)
      (accu:
        (* nombre de chemins, puis listes de mémoïsation : liste des résultats
         * pour seen_fft, puis seen_dac, puis (seen_fft && seen_dac), puis
         * aucun des deux *)
        int * (string * int) list * (string * int) list * (string * int) list *
              (string * int) list
      ) (s: string) =
    let list_to_look_in = accu |> (
      if seen_dac && seen_fft then frth5
      else if seen_fft then snd5
      else if seen_dac then thrd5
      else ffth5
    ) in
    let seen = List.assoc_opt s list_to_look_in in
    match seen with
    | Some(result) ->
        let (a, b, c, d, e) = accu in
        (a+result, b, c, d, e)
    | None ->
      let new_seen_fft = seen_fft || (s = "fft") in
      let new_seen_dac = seen_dac || (s = "dac") in
      let (new_acc, fft, dac, fftdac, none) = List.fold_left (
          explore_depuis new_seen_fft new_seen_dac
      ) accu (List.assoc s graph)
      in
      let to_add = (s, new_acc - (fst5 accu)) in
      if new_seen_fft && new_seen_dac then
        (new_acc, fft, dac, to_add::fftdac, none)
      else if new_seen_fft then
        (new_acc, to_add::fft, dac, fftdac, none)
      else if new_seen_dac then
        (new_acc, fft, to_add::dac, fftdac, none)
      else
        (new_acc, fft, dac, fftdac, to_add::none)
  in
  explore_depuis false false
    (0, [("out", 0)], [("out", 0)], [("out", 1)], [("out", 0)]) "svr"
  |> fst5


let solve (f: string) =
  let input = open_input (Some f) |> parse_input in
  try
    print_int (solve_part_1 input "you");
    print_newline ()
  with
  | Not_found ->
      print_endline ("Partie 1 impossible (Not_found). " ^ 
                     "Ce message d’erreur est normal sur les exemples.");
  try
    print_int (solve_part_2 input);
    print_newline ()
  with
  | Not_found ->
      print_endline ("Partie 2 impossible (Not_found). " ^ 
                     "Ce message d’erreur est normal sur les exemples.");
