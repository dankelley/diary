SELECT entries.entryId, entries.time, entries.entry, tags.tag FROM entries JOIN entry_tag ON entry_tag.entryId = entries.entryId JOIN tags ON entry_tag.tagId = tags.tagId;
