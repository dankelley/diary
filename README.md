# diary
This is planned to be a python script to save diary entries.

Nothing works yet!

I will play a bit with possible UI features, before coding much.
Right now I'm thinking along the following lines.

    diary ACTION ITEM [CATEGORIES]

where ACTION will be a single word, and CATEGORIES will be either a
word or multiple words joined by commas.

Create an uncategorized item, lon and short forms

    diary add "Brush teeth"

Create an item in the 'health' category

    diary add "Brush teeth" health

Create an item in the 'health' and 'habit' categories

    diary add "Brush teeth" "health,habit"

Show health diary items

    diary show health

Both actions and categories will be accepted in abbreviated form, so
long as they are unique.  The actions are predefined as `add` and
`show`, so that is simple.  As for categories, e.g. `ha` would work
for `habit`, but if `handsome` has been entered as category, then
`hab` would be needed.

