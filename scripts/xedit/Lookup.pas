{
  Lookup.pas: generic record lookup for xEdit (FO4Edit), driven by a request file.

  Reads  <IO_DIR>requests.txt  and writes  <IO_DIR>out.txt . Edit the requests, not this script.

  Request lines (blank lines and lines starting with # are ignored):
    file <n>              switch to the n-th loaded file (default 0 = Fallout4.esm)
    id   <hex FormID>     dump one record, e.g.  id 00147BE4
    edid <SIG> <EditorID> dump one record by EditorID, e.g.  edid PERK Blacksmith02
    list <SIG>            one line per record in that group: FormID, EditorID, name
    grepall <SIG> <text>  like grep, but searches every loaded file (tick DLCs in the module list first)
    grep <SIG> <text>     full dump of every record in that group whose dump contains <text> (case-insensitive),
                          e.g.  grep OMOD ArmorPenetration   (can be big for common text)
    npcstats              one line per NPC_ that has a Health or DamageResist property:
                          FormID | EditorID | name | HP | DR | energy resist | level

  Run it from MO2 (Edit executables > FO4Edit) with these Arguments:
    -autoload -autoexit -script:"Z:\home\deck\Repos\Rhodes\scripts\xedit\Lookup.pas" -R:"Z:\home\deck\Games\mo2-lint\tools\our-scripts\xe.log" Fallout4.esm
  xEdit runs inside Proton: it cannot see /tmp, so IO_DIR must be a normal home path.
  Model/texture hash blocks (MODT etc.) are skipped to keep the output readable.
}
unit Lookup;

const
  IO_DIR = 'Z:\home\deck\Games\mo2-lint\tools\our-scripts\';

procedure Dump(e: IInterface; indent: string; sl: TStringList);
var
  i: integer;
  n: string;
begin
  n := Name(e);
  if Pos('Model Information', n) > 0 then
    sl.Add(indent + n + ' = (skipped)')
  else begin
    sl.Add(indent + n + ' = ' + GetEditValue(e));
    for i := 0 to ElementCount(e) - 1 do
      Dump(ElementByIndex(e, i), indent + '  ', sl);
  end;
end;

function Initialize: integer;
var
  req, out, tmp: TStringList;
  i, j, k, p, fi: integer;
  line, cmd, rest, sig, key, av, hp, dr, er: string;
  f, g, r, pr, pp: IInterface;
begin
  Result := 0;
  req := TStringList.Create;
  out := TStringList.Create;
  tmp := TStringList.Create;
  try
    req.LoadFromFile(IO_DIR + 'requests.txt');
    f := FileByIndex(0);
    out.Add('# file 0: ' + GetFileName(f));
    for i := 0 to req.Count - 1 do begin
      line := Trim(req[i]);
      if (line <> '') and (Copy(line, 1, 1) <> '#') then begin
        p := Pos(' ', line);
        if p = 0 then begin
          cmd := line;
          rest := '';
        end else begin
          cmd := LowerCase(Copy(line, 1, p - 1));
          rest := Trim(Copy(line, p + 1, 500));
        end;
        out.Add('');
        out.Add('=== ' + line);
        if cmd = 'file' then begin
          f := FileByIndex(StrToInt(rest));
          out.Add('switched to ' + GetFileName(f));
        end else if cmd = 'id' then begin
          r := RecordByFormID(f, StrToInt('$' + rest), True);
          if Assigned(r) then Dump(r, '', out) else out.Add('NOT FOUND');
        end else if cmd = 'edid' then begin
          sig := Copy(rest, 1, 4);
          key := Trim(Copy(rest, 6, 500));
          g := GroupBySignature(f, sig);
          if Assigned(g) then r := MainRecordByEditorID(g, key) else r := nil;
          if Assigned(r) then Dump(r, '', out) else out.Add('NOT FOUND');
        end else if cmd = 'list' then begin
          g := GroupBySignature(f, rest);
          if not Assigned(g) then out.Add('NO GROUP ' + rest)
          else
            for j := 0 to ElementCount(g) - 1 do begin
              r := ElementByIndex(g, j);
              out.Add(IntToHex(FormID(r), 8) + '  ' + Name(r));
            end;
        end else if cmd = 'grep' then begin
          p := Pos(' ', rest);
          sig := Copy(rest, 1, p - 1);
          key := LowerCase(Trim(Copy(rest, p + 1, 500)));
          g := GroupBySignature(f, sig);
          if not Assigned(g) then out.Add('NO GROUP ' + sig)
          else
            for j := 0 to ElementCount(g) - 1 do begin
              r := ElementByIndex(g, j);
              tmp.Clear;
              Dump(r, '', tmp);
              if Pos(key, LowerCase(tmp.Text)) > 0 then begin
                out.Add('----- ' + IntToHex(FormID(r), 8) + '  ' + Name(r));
                out.AddStrings(tmp);
              end;
            end;
        end else if cmd = 'grepall' then begin
          p := Pos(' ', rest);
          sig := Copy(rest, 1, p - 1);
          key := LowerCase(Trim(Copy(rest, p + 1, 500)));
          for fi := 0 to FileCount - 1 do begin
            g := GroupBySignature(FileByIndex(fi), sig);
            if Assigned(g) then
              for j := 0 to ElementCount(g) - 1 do begin
                r := ElementByIndex(g, j);
                tmp.Clear;
                Dump(r, '', tmp);
                if Pos(key, LowerCase(tmp.Text)) > 0 then begin
                  out.Add('----- [' + GetFileName(FileByIndex(fi)) + '] ' + IntToHex(FormID(r), 8) + '  ' + Name(r));
                  out.AddStrings(tmp);
                end;
              end;
          end;
        end else if cmd = 'npcstats' then begin
          g := GroupBySignature(f, 'NPC_');
          if not Assigned(g) then out.Add('NO GROUP NPC_')
          else
            for j := 0 to ElementCount(g) - 1 do begin
              r := ElementByIndex(g, j);
              hp := '';
              dr := '';
              er := '';
              pr := ElementByPath(r, 'PRPS');
              if Assigned(pr) then
                for k := 0 to ElementCount(pr) - 1 do begin
                  pp := ElementByIndex(pr, k);
                  av := GetElementEditValues(pp, 'Actor Value');
                  if Pos('Health ', av) = 1 then hp := GetElementEditValues(pp, 'Value');
                  if Pos('DamageResist ', av) = 1 then dr := GetElementEditValues(pp, 'Value');
                  if Pos('EnergyResist ', av) = 1 then er := GetElementEditValues(pp, 'Value');
                end;
              if (hp <> '') or (dr <> '') then
                out.Add(IntToHex(FormID(r), 8) + ' | ' + EditorID(r) + ' | ' + GetElementEditValues(r, 'FULL') +
                  ' | HP ' + hp + ' | DR ' + dr + ' | ER ' + er + ' | L ' + GetElementEditValues(r, 'ACBS\Level'));
            end;
        end else
          out.Add('UNKNOWN COMMAND');
      end;
    end;
    out.SaveToFile(IO_DIR + 'out.txt');
  finally
    req.Free;
    out.Free;
    tmp.Free;
  end;
end;

end.
