
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


let parse_input (input: string list) : (int * int) list =
  List.filter_map (
    fun s ->
      if s = "" then
        None
      else
        match List.map int_of_string (String.split_on_char ',' s) with
        | [a; b] -> Some(a, b)
        | _ -> None
  ) input


type point = int * int
type two_points = point * point


let sq a = a*a
let rect_area ((x1, y1): point) ((x2, y2): point) =
  (abs (x2-x1) + 1) * (abs (y2-y1) + 1)


(* cartesian product *)
(* not tail-recursive… *)
let rec ( ** ) (l: 'a list) (l': 'b list) : ('a * 'b) list =
  match l with
  | [] -> []
  | x::q -> (List.map (fun a -> (x, a)) l')@(q ** l')


let rec print_list p l =
  match l with
  | [] -> print_newline (); []
  | x::q -> p x; print_string " "; let _ = print_list p q in l


let solve_part_1 (data: point list) : int =
  data ** data
  |> List.filter_map (
      fun (a, b) -> if a >= b then None else Some(rect_area a b)
    )
  |> List.fold_left (fun a x -> if x > a then x else a) 0


let do_segments_intersect ((a, b) : two_points) ((c, d): two_points) =
  let xa, ya = a in
  let xb, yb = b in
  let xc, yc = c in
  let xd, yd = d in
  let x1, y1 = if xa = xb then xa, yc else xc, ya in
  let x2, x3, y2, y3 = if xa = x1 then xc, xd, ya, yb else xa, xb, yc, yd in
  if x2 <= x1 && x3 <= x1 then false
  else if x2 >= x1 && x3 >= x1 then false
  else if y2 <= y1 && y3 <= y1 then false
  else if y2 >= y1 && y3 >= y1 then false
  else true


(*
let rec is_good_rectangle (data: point list) ((a, b): point * point) : bool =
  if a >= b then false
  else
    let x, y = a in
    let x', y' = b in
    List.for_all (fun x -> false) [] && is_good_rectangle data ((x+1, y), b)


let solve_part_2 (data: point list) : int =
  data ** data
  |> List.filter (is_good_rectangle data)
  |> List.map (
      fun (a, b) -> rect_area a b
    )
  |> List.fold_left (fun a x -> if x > a then x else a) 0
*)


let solve (f: string) =
  let data = parse_input (open_input (Some f)) in
  print_int (solve_part_1 data);
  print_newline ()
